
import subprocess
import sys
from pathlib import Path

project_folder = Path(__file__).parent
interpreter = project_folder / "lovo_interpreter.py"
core_folder = project_folder / "Test_Cases" / "Core"

test_files = sorted(core_folder.rglob("*.uedge"))

if not test_files:
    print("No .uedge files found.")
    sys.exit(1)

passed = 0
failed = 0

print("Running Core Tests...\n")

for test_file in test_files:
    # Error tests are expected to exit with code 1
    is_error_test = "_error_" in test_file.stem
    expected_code = 1 if is_error_test else 0

    result = subprocess.run(
        [sys.executable, str(interpreter), str(test_file)],
        capture_output=True,
        text=True
    )

    if result.returncode == expected_code:
        print(f"[PASSED] {test_file.name}")
        passed += 1
    else:
        print(f"[FAILED] {test_file.name}")
        print(f"Expected exit code: {expected_code}")
        print(f"Actual exit code:   {result.returncode}")

        if result.stderr:
            print("Error:", result.stderr.strip())

        failed += 1

print("\n========== CORE TEST SUMMARY ==========")
print(f"Total:  {len(test_files)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=======================================")
