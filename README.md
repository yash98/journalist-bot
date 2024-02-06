# Journalist Bot
## Problem
Preserving and circulating knowledge across diverse domains can be challenging due to the sheer volume of information generated in various conversations. There is a need for a streamlined process to capture, distill, and present conversational knowledge in a readable format for broader consumption.

## Collaborators
[Yash Malviya](https://github.com/yash98), [Santanu Senapati](https://github.com/KSSSenapati), and [Pushkar Aggrawal](https://github.com/Pushkaraaa), representing Search Relevance at Myntra, are honored to participate. With collective expertise, we aim to innovate solutions. Our team has worked on Gen AI enabled features and Deep Learning tools ex. [MyFashionGPT for Myntra](https://indianexpress.com/article/technology/artificial-intelligence/myntra-microsoft-collaboration-myfashiongpt-azure-9074891/)

## Product Components
1. Arnab (Journalist Bot): Arnab's role is to facilitate discussions, ask relevant questions, and extract valuable knowledge from these conversations.
2. Cataloging Pipeline: Converts Arnab's recordings into a readable format, creating a dynamic encyclopedia.
3. Consumption Platform: A user-friendly platform for exploring, searching, and validating knowledge across domains.

## Expected Outcome
1. Knowledge Preservation: Captures valuable insights, preventing loss.
2. Knowledge Circulation: Breaks down domain barriers, encouraging cross-disciplinary learning.
3. Collaborative Validation: Allows users to cross-reference information for accuracy and give feedback on the recorded information
4. Continuous Learning: A growing encyclopaedia adapting to changing information, fostering continuous learning.

## Approach
1. The bot will interact with users in a non confrontational, curious and friendly manner. Asking relevant questions and keeping the conversation alive and easy. First POC is planned on OpenAI GPT interface however to enhance sticky conversation skills fine-tuning might be needed on data sources such as interviews and podcast transcripts.
2. Bot should have multilingual support to enable wide variety of people to interact with bot and store their knowledge
3. Distilling conversation into a transcript and writing unbiased digestible content such as a blog.
4. Building a wikipedia-like repository of knowledge and keeping relevant data close by cataloging the generated blogs.
5. If multiple instances of the same information are present it can be used to validate the information automatically. If differing opinions on the same topic is present we can detect that there is a chance of subjectivity in the topic
6. The bot should ask questions that do not overwhelm. Do not ask a lot of questions to specific types of users, and it might be a bad experience for those users

## Some Example Use cases
1. Some indigenous skills and cultural heritage such as Yoga, ayurveda, weaving, looming, handcraft techniques etc can be lost to time with advancement of technology, these can be preserved digitally with the help of this bot.
2. Documentation of any tech product or scientific concepts.
3. Journaling a trip.

## Motivation References
1. [https://www.education.gov.in/nep/indian-knowledge-systems](https://www.education.gov.in/nep/indian-knowledge-systems) 
2. [https://www.linkedin.com/pulse/preservation-promotion-indigenous-knowledge-21st-xholiso-ennocent/](https://www.linkedin.com/pulse/preservation-promotion-indigenous-knowledge-21st-xholiso-ennocent/) 
3. [https://www.linkedin.com/pulse/role-indigenous-people-preserving-tradition-knowledge-glowsims/](https://www.linkedin.com/pulse/role-indigenous-people-preserving-tradition-knowledge-glowsims/)

---

## Roadmap

### Datasets, Models, APIs

Tasks to be solved -

1. Translation
   1. If the language model is multilingual it’s not needed
   2. If not
      1. Bing translate API
      2. https://huggingface.co/spaces/facebook/seamless_m4t or https://huggingface.co/openai/whisper-large 
2. TTS
   1. https://huggingface.co/spaces/facebook/seamless_m4t or https://huggingface.co/openai/whisper-large 
3. STT
   1. https://huggingface.co/spaces/facebook/seamless_m4t or https://huggingface.co/openai/whisper-large 
4. Language Model
   1. Microsoft ChatGPT Open AI API
   2. We could Fine tuning LLM to make the conversation more engaging and to make smaller models more accurate for question generation task
      1. Data sets
         1. Podcast datasets (To make the conversation more engaging)
            1. https://zenodo.org/records/7121457#.Y0bzKezMKdY 
            2. https://podcastsdataset.byspotify.com/#:~:text=The%20dataset%20contained%20over%20100%2C000,take%20requests%20to%20access%20it. (No longer available)
         2. We can reuse QnA datasets, instead of generating answers we generate questions. If we have different QnA on a single topic, merging a list of question and answers and expecting the bot to generate the next question is our task
            1. SQUAD dataset is QnA over wikipedia article. We have the topic mentioned in title field https://huggingface.co/datasets/squad/viewer/plain_text/train?p=875
            2. Clustering on QnA Dataset to group similar QnA topics together
      2. Models
         1. Mixtral
         2. Llama
         3. https://huggingface.co/models?pipeline_tag=text-generation&sort=trending 
         4. https://huggingface.co/models?pipeline_tag=question-answering&sort=trending 
5. Vector Search (Context for RAG)
   1. Dataset for retrieval
      1. https://python.langchain.com/docs/integrations/tools/google_search and other search tools
   2. Models
      1. https://huggingface.co/models?pipeline_tag=sentence-similarity&sort=trending 
6. Moderation
   1. https://python.langchain.com/docs/guides/safety/moderation 
   2. Basic word based blacklisting / tagging
   3. Toxic
   4. Dangerous
   5. Bias
   6. Subjectivity
7. Summarisation


### Tech stack

1. Bot
   1. Stream Lit for UI
   2. Langchain and various other libraries for hosting models
2. Cataloging pipeline
   1. Simple python script based indexing pipeline
   2. Periodic crons to generate summary of conversation topics
3. Platform
   1. React for UI
   2. FastAPI for backend
   3. Databases
      1. Elastic search for search index database
      2. Mongo for document store
      3. Or depending on time left, in-memory databases

### Evaluation

Evaluating our prompt (basically generated questions)

User Feedback based : https://medium.com/discovery-at-nesta/how-to-evaluate-large-language-model-chatbots-experimenting-with-streamlit-and-prodigy-c82db9f7f8d9 

Generating questions in different contexts like -

1. Artistic
2. Political
3. Technical

![evaluation question answering agents summary strategy](https://github.com/yash98/journalist-bot/blob/main/docs/img/evaluation-question-answering-agents.png?raw=true)


**Task : Ask better questions**
1. Answering agent here becomes the examiner / evaluator
2. Answering agent is provided a detailed context and exposed to the questioning agent. Answering agent is programmed to be vague and evasive.
3. The questioning agent is exposed to the answering agent and at the end of their interaction we match the input context with the final questioning bot’s summary. SQuaD qualifies here as a prospect benchmarking dataset.

Answering agent can have different personalities like Easy going, difficult to talk to etc

### Control Flows



### Task Breakdown


