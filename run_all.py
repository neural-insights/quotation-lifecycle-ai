import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
UTILS_DIR = ROOT_DIR / "src" / "utils"

def run_script(script_name):
    script_path = UTILS_DIR / script_name
    print(f"Running {script_name} ...")
    result = subprocess.run([sys.executable, str(script_path)], cwd=ROOT_DIR)
    if result.returncode != 0:
        print(f"❌ {script_name} failed with exit code {result.returncode}. Stopping.")
        sys.exit(result.returncode)
    print(f"✅ {script_name} finished successfully.\n")

def main():
    run_script("init_db.py")
    run_script("generate_suppliers.py")
    
    for i in range(5):
        print(f"Consumer run {i+1}/5")
        run_script("consumer.py")
    
    run_script("send_rfqs.py")
    run_script("simulate_quotations.py")
    run_script("generate_training_dataset.py")
    run_script("compile_suppliers_quotations.py")
    run_script("training_lr_model.py")
    run_script("run_won_scoring.py")
    run_script("final_quote_optimizer.py")
    run_script("optimize_quotes_profit.py")

if __name__ == "__main__":
    main()
