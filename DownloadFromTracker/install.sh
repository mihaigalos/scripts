target="invoke_get_movie.sh"
sudo ln -s `realpath "$target"` /usr/local/bin/"$target"
echo alias get=\"$target\" >> ~/.zshrc
