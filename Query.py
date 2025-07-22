# STEP 2: Run User Code and Capture Output
def run_user_code(user_code):
    try:
        exec(user_code, globals())
        return "✅ Code executed successfully."
    except Exception as e:
        return f"❌ Error: {e}"

code_str = '''
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
print(two_sum([2, 7, 11, 15], 9))
'''
print(run_user_code(code_str))
