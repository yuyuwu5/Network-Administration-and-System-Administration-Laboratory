#!/bin/bash

a=$(cat nasa_land/cave/chest)
echo "cave: $a"
b=$(cd nasa_land/village/bookshelf;find -type f -exec du -b {} + | sort -rh | head -n 1 | cut -d '/' -f2)
echo "village: $b"
c=$(cd nasa_land/shop;sed 's/poison/potion/g' list)
$(cp -a nasa_land/shop/ /tmp;cd /tmp/shop;echo $c>answer;sed -i -e 's/ /\n/g' answer)
d=$(cd /tmp/shop;./merchant<answer)
$(cd /tmp/shop; echo $d > final)
echo -n "shop: "
echo $(cd /tmp/shop;cat final|cut -d " " -f55)
$(cd /tmp;rm -rf shop)
$(cp -a nasa_land/castle/ /tmp)
for i in {1..10000}
do
	$(cd /tmp/castle;echo hit >> attack)
done
g=$(cd /tmp/castle; ./boss<attack)
$(cd /tmp/castle;echo $g>final)
echo -n "castle: "
n=$(cd /tmp/castle;wc -w final|cut -d " " -f1)
echo $(cd /tmp/castle; cat final|cut -d " " -f$n)
$(cd /tmp;rm -rf castle)
