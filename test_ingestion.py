from ingestion.dataset_chunker import DatasetChunker

chunker = DatasetChunker()

chunks = chunker.build_chunks()

print("\n------ SAMPLE CHUNK ------\n")

print(chunks[0])
