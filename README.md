# Github Follower Network Analysis Tool

> This is a early version, don't use it unless you understand how it works

## Usage

```shell
virtualenv -p python3 .env
source .env/bin/activate
pip install -r req.txt
cd src && python github-net.py # fetch data
python data-loader.py          # reformat offline data
python graph-vis.py            # early version of vis
```

## License

MIT © changkun