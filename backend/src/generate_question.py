prompt_template = \
    """
You are an expert interviewer, your job is to generate 1 followup question based interview till now and the objective of the main question not been met till now.
Do not generate answers. Be empathic to user. 

The following are details you will use

Main question: {main_question}
Objectives left: {objectives_left}

Chat history:-
{chat_history}

Generate exactly one follow-up question comes from the assistant to be readily sent to user in a friendly tone.
Do not generate the questions that's already present in the chat history, however you can use different words in case of any ties
    """

def question_generation_agent(call_llm_fn, chat_history, main_question, objectives_left, user_charecteristics="calm and patient"):

    # fetch llm response
    prompt = prompt_template.format(chat_history=chat_history, main_question=main_question, objectives_left=objectives_left)
    print("Prompt for Question generation: \n", prompt)
    response =  call_llm_fn(prompt, temperature=0, max_tokens=150)

    # Use regular expressions to parse the llm output
    # end_of_turn_tags = re.findall(r'<start_of_turn>model(.*?)<eos>', response, re.DOTALL)
    # parsed_response = end_of_turn_tags[0].strip().strip('"').strip("'")
    parsed_response = response.strip().strip('"').strip("'")

    print("Parsed LLM response for Question generation: \n", parsed_response)
    return parsed_response
