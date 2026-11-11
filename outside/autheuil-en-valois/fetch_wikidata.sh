for d in 1 2 3 4 5 6 7 8 9; do
  for a in 1 2 3 4 5 6; do
    code=$(curl -sS -m 120 -A 'workshop-research-script/0.2 (one-off toponymy map)' -H 'Accept: text/csv' --data-urlencode query@q_$d.rq https://query.wikidata.org/sparql -o c_$d.csv -w "%{http_code}")
    echo "$d try$a $code $(wc -l < c_$d.csv)"
    if [ "$code" = 200 ] && ! grep -q Exception c_$d.csv; then break; fi
    sleep 75
  done
  sleep 40
done
echo ALLDONE
