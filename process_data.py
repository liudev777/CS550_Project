import csv
import random
import shlex

def parseRedis(input_file, output_csv, n_nodes, client_node_ids):
  available_nodes = list(set(range(n_nodes)) - set(client_node_ids)) # get the storage nodes from list of all nodes

  with open(input_file, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['key', 'value', 'storage_node_id'])
    writer.writeheader()

    for line in infile:
      if not line.startswith("HSET"): # skip non hash files
        continue

      # print(line)
      try:
        data = shlex.split(line.strip())
        key = data[1]

        # parse value as JSON
        fields = data[2:]
        # print(fields)
        value_dict = {}
        
        value_dict = {fields[i]: fields[i + 1].strip('"') for i in range(0, len(fields), 2)}

        # convert to string form to mimic json
        value_str = str(value_dict)

        # assign data to random storage nodes
        random_storage_node = random.choice(available_nodes)

        writer.writerow({
          "key": key,
          "value": value_str,
          "storage_node_id": random_storage_node
        })
      except:
        continue

if __name__ == "__main__":
  parseRedis(
    input_file="import_movies.redis",
    output_csv="data2.csv",
    n_nodes=50,
    client_node_ids=[0, 20, 30, 40]
  )