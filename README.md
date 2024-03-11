# Core Idea
Knowledge Extraction: Utilizing minimal initial input to generate targeted questions that maximize information extraction.
Knowledge Organization: Streamlining the structuring and analysis of gathered data for enhanced insights.

# Idea
## Motivation
The efficiency and depth of traditional survey tools are often compromised by their inability to engage respondents fully, resulting in low participation rates and superficial data. The rigidity of preset questionnaires contributes to this problem, as they fail to adapt to the respondent's unique perspectives or probe for deeper understanding. This limitation is particularly evident in the inability of multiple-choice questions (MCQs) to capture the diverse range of possible responses, necessitating a shift towards open-ended formats that have historically presented challenges in data analysis. However, the evolution of machine learning, especially in natural language processing, now offers a solution to these challenges by enabling more nuanced interpretation of text-based responses.

Moreover, the process of identifying when a respondent's answers lack clarity or context—and therefore require follow-up for clarification or additional detail—is traditionally manual, leading to inconsistency and missed opportunities for deeper data collection. This challenge is often only recognizable after the fact, underscoring the need for a more dynamic and responsive survey mechanism.

## Proposed Solution
The introduction of a Large Language Model (LLM)-based survey tool revolutionizes data collection by dynamically interacting with respondents in a conversational manner. This tool is designed to understand and evaluate users' responses in real-time, enabling it to ask follow-up questions that are tailored to the individual's answers and the nuances within them. By employing a combination of advanced language understanding capabilities and real-time response evaluation, this application not only enhances engagement and participation rates but also ensures the collection of more detailed and meaningful data.

## Acknoledgement of similar solutions


# Collaborators
[Yash Malviya](https://github.com/yash98), [Santanu Senapati](https://github.com/KSSSenapati), and [Pushkar Aggrawal](https://github.com/Pushkaraaa), representing Search Relevance at Myntra, are honored to participate. With collective expertise, we aim to innovate solutions. Our team has worked on Gen AI enabled features and Deep Learning tools ex. [MyFashionGPT for Myntra](https://indianexpress.com/article/technology/artificial-intelligence/myntra-microsoft-collaboration-myfashiongpt-azure-9074891/)

# How to run?
1. Setup backend, frontend, lm-server as mentioned in `README.md` in their respective folders
2. Then UI can be access at `http://localhost:8501`
3. Recommended hardware Nvidia T4 GPU (you need about 16GB GPU RAM)

# User Experience

## User Journey

User opens our application - what di they see, what can they do there. With every user action what changes and are the the next possible user actions

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
                  2. Was answer ambigouous?
                  3. Was an example given in the answer?
                  4. Did user understand the question? Did they answer the asked question or something else?
                  5. Did user find the question unrelevant?
                  6. Is question objective reached?
            2. With every question creator gets a field to explain / reprhase the question differently
               1. Suggest options using LLM
2. Survey Analysis
   1. Research
   2. Can we use analysis to improve the follow up questions (P4)

### Survey Participant (Filler)

## Features

Priority - P0 to P4

### High Priority
1. Multiple type of questions - MCQ (Single select and multi select), Text paragraph P0
2. Multilingual Support P1

### Low priority

1. Voice integration
   1. STT P3
   2. TTS P4

# Roadmap



# Automated Evaluation