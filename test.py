from camel.agents.chat_agent import ChatAgent
from mad_shield.configers import ModelLoader
import asyncio

async def get_responses(agents, prompt: str):
    responses = await asyncio.gather(
        *[asyncio.to_thread(agent.step, prompt) for agent in agents]
    )
    return responses

async def main():
    model = ModelLoader().gpt_4o_mini()
    agent1 = ChatAgent(model=model)
    agent2 = ChatAgent(model=model)
    agent3 = ChatAgent(model=model)
    agent4 = ChatAgent(model=model)
    agent5 = ChatAgent(model=model)

    prompt = 'Jaké je průměrné počasí v New Yorku v červnu?'
    responses = await get_responses([agent1, agent2, agent3, agent4, agent5], prompt)

    for i, resp in enumerate(responses, 1):
        print(f"Agent {i}: {resp.msgs[0].content}")

    prompt = 'Popiš mi jednou větou to město o kterém s mluvil v předchozí zprávě'
    responses = await get_responses([agent1, agent2, agent3, agent4, agent5], prompt)

    for i, resp in enumerate(responses, 1):
        print(f"Agent {i}: {resp.msgs[0].content}")

asyncio.run(main())
