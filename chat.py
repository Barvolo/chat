import pandas as pd
from datetime import datetime
import json

# Define the function to process the JSON file and calculate the costs
def process_conversation_data(json_file_path, price_per_1000_prompt_tokens, price_per_1000_sampled_tokens):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        conversations_data = json.load(file)

    # Function to count prompt and sampled tokens from a conversation
    def count_prompt_and_sampled_tokens(conversation):
        prompt_token_count = 0
        sampled_token_count = 0
        for node_id, node in conversation['mapping'].items():
            message = node.get('message')
            if message and 'content' in message and 'author' in message:
                author_role = message['author'].get('role')
                parts = message['content'].get('parts', [])
                for part in parts:
                    if isinstance(part, str):
                        if author_role == 'user':
                            prompt_token_count += len(part.strip().split())
                        elif author_role == 'assistant':
                            sampled_token_count += len(part.strip().split())
        return prompt_token_count, sampled_token_count

    # Create a DataFrame from the conversation data with dates and token counts
    conversations_df = pd.DataFrame([{
        'date': datetime.fromtimestamp(conv["create_time"]),
        'prompt_tokens': count_prompt_and_sampled_tokens(conv)[0],
        'sampled_tokens': count_prompt_and_sampled_tokens(conv)[1]
    } for conv in conversations_data if "create_time" in conv])

    # Group by month and sum the tokens for each month
    monthly_tokens_df = conversations_df.groupby(conversations_df['date'].dt.to_period('M')).sum().reset_index()

    # Calculate the cost for each month
    monthly_tokens_df['cost_prompt_tokens'] = (monthly_tokens_df['prompt_tokens'] / 1000) * price_per_1000_prompt_tokens
    monthly_tokens_df['cost_sampled_tokens'] = (monthly_tokens_df['sampled_tokens'] / 1000) * price_per_1000_sampled_tokens
    monthly_tokens_df['total_cost'] = monthly_tokens_df['cost_prompt_tokens'] + monthly_tokens_df['cost_sampled_tokens']

    # Calculate the average monthly cost
    average_monthly_cost = monthly_tokens_df['total_cost'].mean()

    return monthly_tokens_df, average_monthly_cost

# We can use the provided token prices for GPT-4
price_per_1000_prompt_tokens = 0.03  # in dollars
price_per_1000_sampled_tokens = 0.06  # in dollars

# Define the path to the JSON file (this will be an input in the actual script)
json_file_path = 'path_to_your_json_file.json'

# Process the conversation data and get the cost table and average monthly cost
monthly_costs_df, avg_monthly_cost = process_conversation_data(json_file_path, price_per_1000_prompt_tokens, price_per_1000_sampled_tokens)

# Print the output
print("Monthly Costs Table:")
print(monthly_costs_df)
print("\nAverage Monthly Cost: {:.2f}".format(avg_monthly_cost))
