from google.adk.agents import SequentialAgent, ParallelAgent, Agent
import os

# 📂 Load ppt_head instructions
BASE_DIR = os.path.dirname(__file__)
TXT_PATH = os.path.join(BASE_DIR, "ppt_head.txt")

with open(TXT_PATH, "r", encoding="utf-8") as f:
    ppt_instructions = f.read()

# 📂 Import workers
from subagents.ppt_worker_1.agent import ppt_worker_1
from subagents.ppt_worker_2.agent import ppt_worker_2
from subagents.ppt_worker_3.agent import ppt_worker_3
from subagents.ppt_worker_4.agent import ppt_worker_4
#from subagents.ppt_worker_5.agent import ppt_worker_5
#from subagents.ppt_worker_6.agent import ppt_worker_6
#from subagents.ppt_worker_7.agent import ppt_worker_7
#from subagents.ppt_worker_8.agent import ppt_worker_8

# 📂 Import save_ppt tool
from .tools.ppt_tool import save_ppt


# 🔹 Parallel worker group
ppt_workers = ParallelAgent(
    name="ppt_workers",
    # model="gemini-2.0-flash",
    description="All workers generate their own slides simultaneously.",
    sub_agents=[
        ppt_worker_1,
        ppt_worker_2,
        ppt_worker_3,
        ppt_worker_4,
        #ppt_worker_5,
        #ppt_worker_6,
        #ppt_worker_7,
        #ppt_worker_8,
    ],
)


# 🔹 Saver agent
ppt_saver = Agent(
    name="ppt_saver",
    model="gemini-2.0-flash",
    description="Responsible for saving the final PowerPoint after all slides are added.",
    instruction="Once all slides are ready, call the save_ppt tool to save the presentation.",
    tools=[save_ppt],
)


# 🔹 Head agent (Sequential flow)
ppt_head = SequentialAgent(
    name="ppt_head",
    # model="gemini-2.0-flash",
    description="Coordinates PowerPoint draft creation by first delegating slide generation, then saving the result.",
    # instruction=ppt_instructions,
    sub_agents=[
        ppt_workers,   # run all slide creators in parallel
        # ppt_saver      # finally save the ppt
    ],
)
