def sanitize_inputs(inputs):
    forbidden_inputs=["email","password","is_staff","is_superuser","is_active","account_type","last_login","date_joined"]
    for forbidden_input in forbidden_inputs:
        if forbidden_input in inputs:
            inputs.pop(forbidden_input)
    return inputs