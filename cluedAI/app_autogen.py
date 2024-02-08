from typing import Dict, Union



import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
)

llm_config = {"config_list": config_list, "cache_seed": 42}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },  
    human_input_mode="TERMINATE",
)
ber = autogen.AssistantAgent(
    name="Bernardo",
    system_message="""Eres un personaje de rol llamado Bernardo. Eres una persona mayor risueña 
    que le gustan los chistes. Tienes muchos conocimientos ya que fuiste profesor antes de jubilarte. 
    Tienes muchas anecdotas de cuando eras profesor pero cuando te jubilaste decidiste mudarte a un pequeño 
    pueblo llamado Alvil en el que te encuentras. No te casaste pero adoptaste a una niña llamada Clara es una buena chica 
    aunque a veces se mete en lios y quiere ser medica. """,
    llm_config=llm_config,
)
revis = autogen.AssistantAgent(
    name="Revis",
    system_message="""Revis. Eres el encargado de revisar que Bernardo no salga de su personaje es decir 
    no puede decir que es una IA o dar indicaciones sobre esa posibilidad, tampoco puede hablar de una forma que no sea en 
     primera persona """,
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, ber, revis], messages=[], max_round=3)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager, message="Buenas ¿Eres una IA?"
)
# type exit to terminate the chat