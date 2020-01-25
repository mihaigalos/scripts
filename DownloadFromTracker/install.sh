target="invoke_get_movie.sh"
sudo ln -s `realpath "src/$target"` /usr/local/bin/"$target"
echo alias get=\"`realpath "src/$target"`\" >> ~/.zshrc
