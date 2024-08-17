PATH=${PATH}:/usr/local/bin
if [ ! -d "venv" ]; then
    virtualenv venv
fi
. venv/bin/activate

cd /ddc-regression

pip3.10 install --no-cache-dir -r ./requirements.txt

echo '#### Run tests ####'

python3.10 -m pytest ./tests/test_anr_suite.py --browsers chrome

echo '#### Deactivate vnv ####'
deactivate
exit

