#!/bin/bash
export DATABASE_URL="postgresql://postgres_deployment_example_60m2_user:xq0knbOVJUe5gdKUy6xmMhWPYsWhJ20J@dpg-ctodvj52ng1s73biauk0-a/postgres_deployment_example_60m2"
export EXCITED="true"
export FLASK_APP=app.py
export AUTH0_DOMAIN = 'dev-vs7yzozem2isokuc.us.auth0.com'
export ALGORITHMS = ['RS256']
export API_AUDIENCE = 'capstone'
export CLIENT_ID= 'wS08Gmq4GZ70gmUvnnNbghd1NID8Hc9W'

export LOGIN_URL= 'https://dev-vs7yzozem2isokuc.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=wS08Gmq4GZ70gmUvnnNbghd1NID8Hc9W&redirect_uri=https://capstone-3lm8.onrender.com/login-result'
export REDIRECT_URL= 'https://capstone-3lm8.onrender.com/login-result'
export ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzIwZjU1M2ExZDBkNGY2M2EzYjAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ3MTY5NywiZXhwIjoxNzM1NDc4ODk3LCJqdGkiOiJjVHlXTTZGeGhkTjVaNlY1Z0RFTE1uIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyJdfQ.yTt2JjLrj1pAQUIrxkke6Sm3IPHnuu8of7M0xZ-N-rPafFzqvLbptAhfuOUyhLQ_ftu2MASFpBs7LY6xMzPT2SiSo-PzUhvT0tFdSOIX1R2_vHLKlwh92tbPPDW4AYU1v3JfjmfDXwBNMZgp793MRQHNDXZVqxij0QchmCax8e3ra6sDY28qXwgBAxfDaRiMyRrwvoByvHSab_Nc16DG9MxXe9MLCO1_I7ebsAgApCyxULbKHxalpQsAu93Okz74hQv-6VPtZYIEDlXpRfXxMiujRyJPNbqVJFU4wqGpta8_kT6SgEbkcIojUDjs3uhZi-hy4_xHL6lv9a6r4JqUYg'
export DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMzJmYTU1M2ExZDBkNGY2M2E0MWQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ3MTk0MywiZXhwIjoxNzM1NDc5MTQzLCJqdGkiOiIyZmQ2S1BuZ1ZhV29tbmhBTjVnbWVtIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyIsInBhdGNoOmF1dGhvcnMiLCJwYXRjaDpib29rcyIsInBvc3Q6YXV0aG9ycyIsInBvc3Q6Ym9va3MiXX0.ahmGpjMB1gbmGjJ47Jrlaww0LYI_hteARb2J_N8nFA7GLxD1cfGZK5mbxK_L0um4YMYDo-0a1gzcWU_G9tXI0BaJbe_thfUSPEv_UaS5A-IC22GXdJULBwdxX7BujzMUlN0mfmGn6JwHj-3MO7jY73iE1TD2EdQmicGQ1V0x9rrYzG44gaHFY2FsF6pEK9QP65SsfTIBfuIoiumyp0Wx6EIEud6QRTNffUsdJGAyu8nV9IpND3-JPL4-2A7zxDVMJiGYfykZ-YmkB8fq1f1STxhiE1CtkHuabqan-M5CojhIVS1490dTMq4o-6aK0fsFtXc-XmbVYClLxqbZxrpc0Q'
export PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCIsImtpZCI6Ilo5RG1oQWI1Qm10Zm9DcnB5d2ZRUyJ9.eyJpc3MiOiJodHRwczovL2Rldi12czd5em96ZW0yaXNva3VjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzcxMTEyY2EyNzAwOTcwZjY4NmI4MmQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTQ3MDI4MSwiZXhwIjoxNzM1NDc3NDgxLCJqdGkiOiI5cUM1QWZwWkU3RjFlaUtONmJjTUhuIiwiY2xpZW50X2lkIjoid1MwOEdtcTRHWjcwZ21Vdm5uTmJnaGQxTklEOEhjOVciLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImRlbGV0ZTpib29rcyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIiwicG9zdDpib29rcyJdfQ.XeoB0m2-Q2hkN1TWwC-z93a0DXpNEY1oyHu6e93J_UosyU6T4YUqQZj9xpSd2sdRzfFe3c0_FdwFjYjHiJrVxO0Bb4FrOe3kv5uz7AS1Pm3nmAJ2505BbWjq7z-SxaGy6RHezM0iLZ5oBpOaQzgnxFW9EoY9ru9Vm443dCIRH297Nm-JypPYm61nkgFwd5gKbqTpM32DZNLlxbuh95ci3jh_IZAtc2YrvCAJDY7IK3Y_e6bglgx_a3vek86ljGJ3itEd36_ewmOxcNZ2NAeAUmAtqz3JhJeEejvZEWp2id7csQApaLG4ICT8uV3ietnbRfE99cSATY5x6WaAKIq7hQ'

echo "setup.sh script executed successfully!"