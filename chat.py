from flask import Flask, request, render_template
import pandas as pd
from datetime import datetime
import json
from nltk.tokenize import word_tokenize

app = Flask(__name__, static_url_path='', static_folder='static')

# Define the function to process the conversation data and calculate the costs
def process_conversation_data_from_data(conversations_data, price_per_1000_prompt_tokens, price_per_1000_sampled_tokens, start_date=None, end_date=None):
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
                        # Tokenize the part using NLTK's word_tokenize
                        tokens = word_tokenize(part.strip())
                        if author_role == 'user':
                            prompt_token_count += len(tokens)
                        elif author_role == 'assistant':
                            sampled_token_count += len(tokens)
        return prompt_token_count, sampled_token_count



    # Convert start and end dates to datetime objects if they are not None and are in string format
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Create a DataFrame from the conversation data with dates and token counts
    conversations_df = pd.DataFrame([{
        'date': datetime.fromtimestamp(conv["create_time"]),
        'prompt_tokens': count_prompt_and_sampled_tokens(conv)[0],
        'sampled_tokens': count_prompt_and_sampled_tokens(conv)[1]
    } for conv in conversations_data if "create_time" in conv])

    # If start_date and/or end_date are specified, filter the DataFrame accordingly
    if start_date:
        conversations_df = conversations_df[conversations_df['date'] >= start_date]
    if end_date:
        conversations_df = conversations_df[conversations_df['date'] <= end_date]
    # Group by month and sum the tokens for each month, specifying numeric_only to avoid the warning
    monthly_tokens_df = conversations_df.groupby(conversations_df['date'].dt.to_period('M')).sum(numeric_only=True).reset_index()
    # Calculate the cost for each month
    monthly_tokens_df['cost_prompt_tokens'] = (monthly_tokens_df['prompt_tokens'] / 1000) * price_per_1000_prompt_tokens
    monthly_tokens_df['cost_sampled_tokens'] = (monthly_tokens_df['sampled_tokens'] / 1000) * price_per_1000_sampled_tokens
    monthly_tokens_df['total_cost'] = monthly_tokens_df['cost_prompt_tokens'] + monthly_tokens_df['cost_sampled_tokens']

    # Calculate the average monthly cost
    average_monthly_cost = monthly_tokens_df['total_cost'].mean()

    return monthly_tokens_df, average_monthly_cost

# The route for the main page with the upload form
@app.route('/')
def index():
    return render_template('upload.html')

# The route that will process the uploaded file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('upload.html', error="No file part")

    file = request.files['file']
    if file.filename == '':
        return render_template('upload.html', error="No selected file")
    
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    if file:
        # Read the content of the file
        conversations_data = json.load(file.stream)
        monthly_costs_df, avg_monthly_cost = process_conversation_data_from_data(
            conversations_data,
            price_per_1000_prompt_tokens=0.03,  # in dollars
            price_per_1000_sampled_tokens=0.06,  # in dollars
            start_date=start_date,  # Start date from the form
            end_date=end_date       # End date from the form
            
        )
        
        # Calculate savings or extra spent
        flat_rate = 20  # Flat rate per month
        monthly_costs_df['savings'] = flat_rate - monthly_costs_df['total_cost']

        # Calculate the total savings over all months
        total_savings = monthly_costs_df['savings'].sum()
        
        # Convert DataFrame to HTML
        results_html = monthly_costs_df.to_html(index=False, classes='table table-striped')
        
        # Prepare savings analysis data for the template
        savings_analysis = monthly_costs_df[['date', 'savings']].to_dict('records')
        
        # Prepare the data for the chart
        labels = [record['date'].strftime('%B %Y') for record in savings_analysis]
        data = [record['savings'] for record in savings_analysis]

        # Render the results in a new template
        return render_template('results.html', 
                               results_table=results_html, 
                               average_cost=avg_monthly_cost, 
                               savings_analysis=savings_analysis,
                               total_savings=total_savings,
                               chart_labels=labels,
                               chart_data=data,
                               start_date=start_date,  # Pass start date to the template
                               end_date=end_date       # Pass end date to the template
                               )

if __name__ == '__main__':
    app.run(debug=True)


