if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Teampir/d-n-1-f.git /Pirate
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Pirate
fi
cd /Pirate
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
