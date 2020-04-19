#! /bin/bash

POSTER="lotr/lotr3.jpg"

# convert to 3x3
POSTER_SMALL="tmp_poster_small.png"
convert ${POSTER} -resize 3x3\! ${POSTER_SMALL}

# convert to 1000x1000
POSTER_1K="tmp_poster_1k.png"
convert ${POSTER_SMALL} -resize 1000x1000 ${POSTER_1K}

# crop circle
POSTER_CIRCLE="tmp_poster_circle_1k.png"
convert -size 1000x1000 xc:transparent -fill "${POSTER_1K}" -draw "circle 500,500 500,0" -crop 1000x1000+0+0 +repage ${POSTER_CIRCLE}

# resize circle
POSTER_CIRCLE_SMALL="tmp_poster_circle_small.png"
convert ${POSTER_CIRCLE} -resize 110x110 ${POSTER_CIRCLE_SMALL}

# add white border
POSTER_CIRCLE_SMALL_BORDER="tmp_poster_circle_small_border.png"
convert ${POSTER_CIRCLE_SMALL} -bordercolor white -border 445 ${POSTER_CIRCLE_SMALL_BORDER}

# add poster to movie circle
# composite ${POSTER_CIRCLE_SMALL_BORDER} -compose Multiply resize1000.png out.png
