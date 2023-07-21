start:
	sudo docker start VICTIM 2>/dev/null
	sudo docker start attacker 2>/dev/null

attacker_LLC: start
	sudo docker cp ATTACKER/launch_LLC.sh attacker:/root
	sudo docker exec -d attacker sh -c "cd /root && chmod +x launch_LLC.sh &&./launch_LLC.sh &" 

attacker_LOCKING: start
	sudo docker cp ATTACKER/launch_LOCKING.sh attacker:/root
	sudo docker exec -d attacker sh -c "cd /root && chmod +x launch_LOCKING.sh && nohup ./launch_LOCKING.sh"

NORMAL:
	sudo docker cp VICTIM/launch.sh VICTIM:/root
	sudo docker exec -it VICTIM sh -c "cd /root && chmod +x launch.sh  && ./launch.sh normal_behaviour"

LLC : start attacker_LLC
	sudo docker cp ./VICTIM/launch.sh VICTIM:/root
	sudo docker exec -it VICTIM sh -c "cd /root && chmod +x launch.sh  && ./launch.sh LLC_effect"
	sudo docker stop attacker

ATOMIC_LOCKING : start  attacker_LOCKING
	sudo docker cp ./VICTIM/launch.sh VICTIM:/root
	sudo docker exec -it VICTIM sh -c "cd /root && chmod +x launch.sh  && ./launch.sh LOCKING_effect"
	sudo docker stop attacker

GRAPHS:
	sudo docker cp VICTIM:/root/normal_behaviour.txt /stats/
	sudo docker cp VICTIM:/root/LLC_effect.txt  /stats/
	sudo docker cp VICTIM:/root/LOCKING_effect.txt /stats/
	python3 stats.py


