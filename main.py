def main(url):
    
    # Download data
    project0.fetchincidents(url)
    file=fetchincidents(url)
    
    # Extract Data
    incidents = project0.extractincidents(file)
	
    # Create Dataase
    db = project0.createdb()
	
    # Insert Data
    project0.populatedb(incidents)
	
    # Print Status
    project0.status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="The arrest summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)


