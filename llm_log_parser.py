import pandas as pd
import openai
from time import sleep

# === Configuration ===
openai.api_key = ""  # 建議從環境變數讀取較安全

# === Prompt Template ===
def build_prompt(note):
    return f"""
請根據下列智慧工廠維護紀錄，判斷可能的機台故障原因，並預測是否近期需要再次維修：

維護紀錄：{note}

請以繁體中文輸出，格式如下：
1. 故障推論：
2. 預測建議：
"""

# === Main LLM Call ===
def analyze_log(note):
    prompt = build_prompt(note)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是智慧工廠維修專家，擅長解讀維修日誌與預測潛在風險"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error"

# === Load Log Dataset ===
df = pd.read_csv("simulated_maintenance_logs.csv")
df["llm_analysis"] = ""

# === Run Analysis on Sample Logs ===
for i in range(min(10, len(df))):  # 建議先跑前10筆測試
    note = df.loc[i, "maintenance_notes"]
    print(f"Analyzing: {note}")
    result = analyze_log(note)
    df.loc[i, "llm_analysis"] = result
    print(result)
    sleep(1.5)  # 降低API速率，避免被限流

# === Export Result ===
df.to_csv("llm_maintenance_analysis.csv", index=False)
print("✅ 分析完成，輸出存為 llm_maintenance_analysis.csv")
