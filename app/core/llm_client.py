import os
import openai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.client = openai.OpenAI(api_key=api_key)

    def process_with_llm(self, pdf_text: str, prompt: str) -> list:
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": f"Here is the credit card statement text:\n\n{pdf_text}"}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1,
                max_tokens=2000
            )
            llm_response = response.choices[0].message.content.strip()
            return self._parse_llm_response(llm_response)
        except Exception as e:
            print(f"LLM processing error: {e}")
            return []

    def _parse_llm_response(self, response: str) -> list:
        transactions = []
        lines = response.strip().split('\n')
        table_lines = []
        for line in lines:
            if line.startswith('|') and '---' not in line and 'Date' not in line:
                table_lines.append(line)
        current_date = ""
        for line in table_lines:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(cells) >= 4:
                date = cells[0].strip()
                merchant = cells[1].strip()
                amount = cells[2].strip()
                category = cells[3].strip()
                if date:
                    current_date = date
                if merchant and amount and category:
                    transactions.append({
                        'Date': current_date,
                        'Merchant': merchant,
                        'Amount': amount,
                        'Category': category
                    })
        return transactions 