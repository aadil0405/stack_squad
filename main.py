import json
import re
import random_responses
import socketio
import asyncio


# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")

#socket io server instance
sio = socketio.AsyncServer()
app = socketio.AsyncioMiddleware(sio)


def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Check if input is empty
    if input_string == "":
        return "Please type something"

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_responses.random_string()

#function to handle incoming message
async def message_handler(sid, data):
    user_input = data['message']
    if not user_input.strip():
        await sio.emit('bot_response', {'message': 'Please type something'}, room=sid)
        return
    bot_response = get_response(user_input)
    await sio.emit('bot_response', {'message': bot_response}, room=sid)

# Attach the event handler for 'message' events
sio.on('message', message_handler)

# Main asyncio event loop to run the Socket.IO server
async def main():
    # Create an aiohttp web application
    app = socketio.AsyncioMiddleware(sio)
    web_app = web.Application()
    web_app.add_routes([web.static('/', './public')])  # Replace './public' with your frontend directory
    web_app.router.add_route('GET', '/', index)
    web_app.router.add_route('GET', '/socket.io/', app)
    web_app.router.add_route('POST', '/socket.io/', app)

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()

if __name__ == '__main__':
    asyncio.run(main())



#while True:
#    user_input = input("User: ")
#    print("ChatBot:", get_response(user_input))
