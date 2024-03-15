# Dynamic Survey
## Core Idea
Knowledge Gathering: Utilizing minimal initial input to generate targeted questions that maximize information gathering by having a dialogue with people.
Knowledge Organization: Streamlining the structuring and analysis of gathered data for enhanced insights.

Another use case with a lot of overlap with the current one: [Journalist bot - conduct interview with people to distill and preserve niche and novel information](https://github.com/yash98/journalist-bot/blob/main/journalist-bot-original-idea.md)

# Current Use Case

## Motivation
Traditionally, surveys have predominantly consisted of multiple-choice and close-ended short answer questions. This is partly because analyzing responses to open-ended questions can be challenging. However, advancements in Natural Language Processing (NLP), such as Large Language Models (LLMs), have made it easier to tackle this issue. The efficiency and depth of traditional survey tools are often compromised by their inability to engage respondents fully, resulting in low participation rates and superficial data. The rigidity of preset questionnaires contributes to this problem, as they fail to adapt to the respondent's unique perspectives or probe for deeper understanding. However, the evolution of machine learning, especially in natural language processing, now offers a solution to these challenges by enabling more nuanced interpretation of text-based responses.

Open-ended questions allow survey participants to express their thoughts and opinions more freely, potentially revealing insights that the survey creator hadn't anticipated. In contrast, multiple-choice questions can inadvertently influence responses by presenting predefined options. However, open-ended questions also pose challenges, such as vagueness or lack of specificity, which may hinder the extraction of useful insights. Moreover, the process of identifying when a respondent's answers lack clarity or context—and therefore require follow-up for clarification or additional detail—is traditionally manual, leading to inconsistency and missed opportunities for deeper data collection. In such cases, follow-up questions can help prompt participants to provide more specific information. Our focus is on addressing the challenges associated with open-ended questions, particularly regarding vagueness and staying aligned with the purpose of the question. This challenge is often only recognizable after the fact, underscoring the need for a more dynamic and responsive survey mechanism.

## Solution
The introduction of a Large Language Model (LLM)-based survey tool revolutionizes data collection by dynamically interacting with respondents in a conversational manner. This tool is designed to understand and evaluate users' responses in real-time, enabling it to ask follow-up questions that are tailored to the individual's answers and the nuances within them. By employing a combination of advanced language understanding capabilities and real-time response evaluation, this application not only enhances engagement and participation rates but also ensures the collection of more detailed and meaningful data.

## Demo
[![Dynamic Survey Demo](https://github.com/yash98/journalist-bot/blob/main/docs/img/dynamic-survey-demo.png?raw=true)](https://www.youtube.com/watch?v=1kTk0raKQX8 "Dynamic Survey Demo")

# How to run?
1. Setup backend, frontend, lm-server as mentioned in `README.md` in their respective folders
2. Then UI can be access at `http://localhost:8501`
3. Recommended hardware Nvidia T4 GPU (you need about 16GB GPU RAM)

# User Experience

## User Journey

User opens our application - what do they see, what can they do there. With every user action what changes and are the the next possible user actions

### Survey Creator

1. Create a new Survey
   1. Add topic
      1. Describe topic
   2. Add questions
      1. We will suggest some possible questions based on the topic and previously added questions
      2. Select question type -
         1. MCQ
         2. Text
            1. Creator specified configs -
               1. Maximum follow up question depth
               2. Question objective
               3. Criteria to evaluate whether to ask follow up questions or not
                  1. Was answer specific?
                  2. Was answer ambiguous?
                  3. Was an example given in the answer?
                  4. Did user understand the question? Did they answer the asked question or something else?
                  5. Did user find the question irrelevant?
                  6. Is question objective reached?
            2. With every question creator gets a field to explain / rephrase the question differently
               1. Suggest options using LLM
2. Survey Analysis
   1. Research
   2. Can we use analysis to improve the follow up questions (P4)

### Survey Participant (Filler)

Basic UI were user answers the configured questions one after the other

# Solution Details

## Survey Creation (High Level Design)
![Survey Creation](https://github.com/yash98/journalist-bot/blob/main/docs/img/survey-creator-diagram.png?raw=true)

## Survey Bot Chain of Agents (High Level Design)
![Survey Bot Chain of Agents](https://github.com/yash98/journalist-bot/blob/main/docs/img/survey-filler-diagram.png?raw=true)

## Tech Architecture

![Tech Architecture](https://github.com/yash98/journalist-bot/blob/main/docs/img/dynamic-survey-tech-arch.png?raw=true)

A fronted app written using streamlit can be used to create surveys and for filling survey
The fronted app interacts with a backend service written using FastAPI
The backend service contains the survey bot which use two agent - objective met agent, question generation agent to generate follow up questions wherever needed 
The data for survey questions, conversation done with a survey participant and state of survey is stored in mongodb

# Automated Evaluation

## Objective Met Agent
We generated 20 surveys with questions (about 3 questions each survey) and associated motivation (some motivation were also added manually). We generated associated survey participant descriptions and question answers conversation based on survey questions. Then we sliced the conversations into multiple as the expected input by the agent and manually annotated the data (i.e. manually marked which conversation slice had which objectives met). This gave use approximately 100 test cases which we used to evaluate different prompts and thresholds for prompts    

All the generations were done by prompt engineering and using GPT

## Features

Priority - P0 to P4

### High Priority
1. Multiple type of questions
   1. MCQ (Single select and multi select) P1
   2. Text paragraph P0
2. Multilingual Support P1
3. Survey Bot (Collection of agents) P0
4. Authentication P1

### Low priority

1. Voice integration
   1. STT P3
   2. TTS P4

# Collaborators
[Yash Malviya](https://github.com/yash98), [Santanu Senapati](https://github.com/KSSSenapati), and [Pushkar Aggrawal](https://github.com/Pushkaraaa), representing Search Relevance at Myntra, are honored to participate. With collective expertise, we aim to innovate solutions. Our team has worked on Gen AI enabled features and Deep Learning tools ex. [MyFashionGPT for Myntra](https://indianexpress.com/article/technology/artificial-intelligence/myntra-microsoft-collaboration-myfashiongpt-azure-9074891/)