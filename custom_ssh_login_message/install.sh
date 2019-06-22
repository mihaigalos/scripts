sudo apt -y install neofetch

osmc_distro_ascii=$(realpath osmc_distro.ascii)

cat <<EOF >> ~/.zshrc               
neofetch --underline off --color_blocks off  --ascii $osmc_distro_ascii --ascii_colors 4 --gap 7
EOF

touch ~/.hushlogin # disable other login info
