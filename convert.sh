for file in orig/*.txt
do
    ofile=`basename $file`
    echo "converting $file to converted/$ofile"
    chordpro.py $file > converted/$ofile
done
