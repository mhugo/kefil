#!/bin/bash

COUPONS_CSV=coupons.csv
TEMPLATE_SVG=coupon_template.svg

n=1
while read -r line
do
    F=$(printf "coupon_%03d.pdf" $n)
    ID=$(echo $line | awk -F ',' '{print($1)}')
    TEXT=$(echo $line | awk -F ',' '{print($2)}')
    echo $ID, $TEXT
    sed -e "s/{{ID_COUPON}}/${ID}/" -e "s/{{OFFRE_COUPON}}/${TEXT}/" $TEMPLATE_SVG > tmp.svg
    inkscape tmp.svg --export-type=pdf --export-filename=$F
    n=$((n + 1))
done < $COUPONS_CSV

# pdfjam --nup 2x4 coupon_???.pdf --outfile coupons_a4.pdf
