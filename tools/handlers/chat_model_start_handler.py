from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen

def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))

class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self,
                            serialized,
                            messages,
                            **kwargs):
        print("\n\n\n\n========Sending Messages========\n\n")

        for message in messages[0]:
          match message.type:
              case "human":
                  boxen_print(message.content, title=message.type, color="yellow")
              case "system":
                  boxen_print(message.content, title=message.type, color="blue")
              case "assistant":
                  boxen_print(message.content, title=message.type, color="green")
              case "function":
                  boxen_print(message.content, title=message.type, color="magenta")
              case _ if message.type == "ai" and "function_call" in message.additional_kwargs:
                  call = message.additional_kwargs["function_call"]
                  boxen_print(
                    f"Running tool call: {call['name']} with args {call['arguments']}",
                    title=message.type, color="red"
                  )
              case "ai":
                  boxen_print(message.content, title=message.type, color="white")
              case _:
                  boxen_print(message.content, title=message.type, color="gray")

        print("\n\n========End of Messages========\n\n")
