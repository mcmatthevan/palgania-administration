cd /home/minecraft/palgania_save
#mv b c
#cp server_sav b
#git pull
tar czfv /home/minecraft/palgania_save/server_sav /home/minecraft/server
python3 encrypt.py
mv server_sav.enc server_sav
git rm -r --cached github_saves
git commit -am "clear files commit"
git push
rm github_saves/*
split -b 90M server_sav github_saves/server_sav_
#git add github_saves
git config core.filemode false
./push_oby.py
NOW=$(date '+%F_%H:%M:%S')
echo "$NOW" > last_save
cd /home/minecraft/
mv palgania_save ancsav
git clone git@palgit:mcmatthevan/palgania_save.git --depth 2
#mv ancsav/b palgania_save/
#mv ancsav/c palgania_save/
mv ancsav/last_save palgania_save/
mv ancsav/push_oby.py palgania_save/
mv ancsav/server_sav palgania_save/
cp ancsav/save.sh palgania_save/
#git commit -am "$NOW"
#git push
rm -rf ancsav
