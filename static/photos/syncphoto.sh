directory=$1

if hash drive; then
    cd $directory
    drive push
    echo "synced!"
else
    echo "drive does not exist, cannot sync"
fi
