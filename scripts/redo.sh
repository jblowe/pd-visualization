#git clone https://github.com/jblowe/pd-visualization.git
#cd pd-visualization/
#cd scripts/
#pip install colour
#cp ~/cspace_django_project/common/Counter.py .
#pip install "numpy<1.10"
python get_captures.py /tmp/4solr.pahma.public.csv ../data/captures.json
python get_genres.py /tmp/4solr.pahma.public.csv ../data/genres.json ../data/item_genres.json
python get_dates.py /tmp/4solr.pahma.public.csv ../data/centuries.json ../data/item_centuries.json century
python get_collections.py /tmp/4solr.pahma.public.csv ../data/collections.json ../data/item_collections.json

#python download_images.py ../data/captures.json ../img/items/ thumbnail

python get_color_data.py ../data/captures.json ../img/items/ ../data/itemp_hsl.json 3 > pct.txt
python get_colors.py ../data/itemp_hsl.json ../data/colors.json ../data/item_colors.json

python stitch_images.py ../data/ ../img/items/ ../img/ 100 10 10 default 50 20 3 30000
python stitch_images.py ../data/ ../img/items/ ../img/ 100 10 10 centuries 50 20 3 30000
python stitch_images.py ../data/ ../img/items/ ../img/ 100 10 10 collections 50 20 3 30000
python stitch_images.py ../data/ ../img/items/ ../img/ 100 10 10 colors 50 20 3 30000
python stitch_images.py ../data/ ../img/items/ ../img/ 100 10 10 genres 50 20 3 30000


