python makedata.py

for i in $(seq 10); do
	python runstan.py data.npz model.stan chain$i.npz
done


