# Dynamic Survey

![LOGO](https://github.com/yash98/journalist-bot/blob/main/docs/img/creator-ui.drawio.png?raw=true](https://github.com/yash98/journalist-bot/blob/main/docs/img/IMG-20240406-WA0010.jpg?raw=true
))

## Core Idea
Knowledge Gathering: Generate targeted questions that maximize information gathering by having a dialogue with people.

## Motivation

Surveys predominantly use closed-ended questions
Closed-ended questions lack engagement, leading to low participation and superficial insights.
They fail to adapt to respondents' perspectives.
Generative AI can interact with users within their context and also enable nuanced interpretation of text-based responses.

## Solution

Introduce an LLM-based survey tool which interacts dynamically, understanding and evaluating responses in real-time.
Tailors follow-up questions based on individual answers and nuances.
This leads to
Enhances engagement, participation rates, and ensures meaningful and deeper insights.

## Demo
[![Dynamic Survey Demo](https://github.com/yash98/journalist-bot/blob/main/docs/img/dynamic-survey-demo.png?raw=true)](https://www.youtube.com/watch?v=1kTk0raKQX8 "Dynamic Survey Demo")

## Presentation
[Presentation Link](https://docs.google.com/presentation/d/1c0cKJ5f5kSuq8tplEJpUmQDFVEhOC0W2ookLA_vHAYM/edit#slide=id.g26bd4b1d05e_0_2)

# How to run?
1. Setup backend, frontend, lm-server as mentioned in `README.md` in their respective folders
2. Then UI can be access at `http://localhost:8501`
3. Recommended hardware Nvidia T4 GPU (you need about 16GB GPU RAM)

# User Experience

## User Journey

User opens our application - what do they see, what can they do there. With every user action what changes and are the the next possible user actions

### Survey Creator

1. Create a new Survey
   Add fixed questions, maximum followups allowed, and the fixed question's objective.
       Creator specified configs -
               1. Maximum follow up questions allowed per fixed question
               2. Objectives to evaluate whether to ask follow up questions or not
                  1. Was answer specific?
                  2. Was answer ambiguous?
                  3. Was an example given in the answer?
                  4. Did user understand the question? Did they answer the asked question or something else?
                  5. Did user find the question irrelevant?
                  6. Is question objective reached?



### Survey Participant (Filler)

Basic UI were user answers the configured questions one after the other

# Solution Details

## Survey Creation (High Level Design)
![Survey Creation](https://github.com/yash98/journalist-bot/blob/main/docs/img/creator-ui.drawio.png?raw=true)

## Multiagent system
![Survey Bot Chain of Agents](https://github.com/yash98/journalist-bot/blob/main/docs/img/multiagent-flow.drawio.png?raw=true)

## Tech Architecture

![Tech Architecture](https://github.com/yash98/journalist-bot/blob/main/docs/img/hld-new.drawio.png?raw=true)

A fronted app written using streamlit can be used to create surveys and for filling survey
The fronted app interacts with a backend service written using FastAPI
The backend service contains the survey bot which use two agent - objective met agent, question generation agent to generate follow up questions wherever needed
The data for survey questions, conversation done with a survey participant and state of survey is stored in mongodb.
For LLM capabilities we host the model using vLLM which comes with a lot of LLM inference optimisations out of the box. 
LLM used is quantised gemma-7b-it

# Automated Evaluation

## Objective Met Agent

Test bench creation
1. 20 surveys
2. User personas
3. Survey simulation
4. Manual annotation within conversations for objective met agent

All the generations were done by prompt engineering and using Mixtral 8x7B

We generated 20 surveys with questions (about 3 questions each survey) and associated motivation (some motivation were also added manually). We generated associated survey participant descriptions and question answers conversation based on survey questions. Then we sliced the conversations into multiple as the expected input by the agent and manually annotated the data (i.e. manually marked which conversation slice had which objectives met). This gave use approximately 100 test cases which we used to evaluate different prompts and thresholds for prompts    


## Features
1. Huggingface models integrated (tested on Gemma-7B)
2. ChatGPT API integrated
3. vLLM optimised server - batched requests, quantised, faster kernel
4. Google Auth for survey fillers

Priority - P0 to P4

### High Priority
1. Multiple type of questions
   1. MCQ (Single select and multi select) P1
   2. Text paragraph P0
2. Multilingual Support P1
3. Survey Bot (Collection of agents) P0
4. Authentication P1
5. 

### Low priority

1. Voice integration
   1. STT P3
   2. TTS P4

# Collaborators
Members from Search Relevance Team at Myntra, built this to present at a Hasgeek hackathon . With collective expertise, we aim to innovate solutions. Our team has worked on Gen AI enabled features and Deep Learning tools ex. [MyFashionGPT for Myntra](https://indianexpress.com/article/technology/artificial-intelligence/myntra-microsoft-collaboration-myfashiongpt-azure-9074891/)
