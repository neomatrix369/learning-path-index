from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import CSVReader
import weaviate
from loguru import logger
import pandas as pd
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.weaviate  import WeaviateVectorStore


class VectorDB:
    """
    Create a weaviate vector database from a the Learning Path Index csv file.
    """
    def __init__(  
        self,
        data_path: str,
        index_name: str,
    ):
        """
        Initialize the VectorDB class.
        
        Args:
            data_path: str, path to the Learning Path Index csv file.
            index_name: str, name of the index to create.   
        Output:
            None
        """
        self.data_path = data_path
        self.index_name = index_name

        try:
            self.client = weaviate.connect_to_embedded()
        except weaviate.exceptions.WeaviateConnectionError as e:
            raise ConnectionError(f"Failed to connect to Weaviate: {str(e)}")

    def disconnect(self):
        """
        Disconnect from the Weaviate vector database.
        """
        if self.client:
            self.client.close()  # Assuming the client has a close method
            logger.info("Disconnected from the Weaviate vector database.")
        else:
            logger.warning("No active connection to disconnect.")

    
    def LPI_loader(self):
        """
        Load the Learning Path Index csv file.
        """
        # Load data  csv file
        df = pd.read_csv(self.data_path)

        # Use the CSVReader to load the data and load each row as a document by setting concat_rows=False
        parser = CSVReader(concat_rows=False)
        file_extractor = {".csv": parser}  # Add other CSV formats as needed
         
        # Load the documents
        documents = SimpleDirectoryReader(
            input_files = [self.data_path], file_extractor=file_extractor
            ).load_data()

        logger.debug(documents[1])


        # Adding Metadata to the documents
        start = 1
        for _, row in df.iterrows():
            documents[start].metadata = {'source': row['Source'], 'Course': row['Course_Learning_Material'], 'Module' : row['Module'] }
            start += 1
        
        return documents

    def vector_db_creation(self):
        """
        Create a weaviate vector database from the Learning Path Index csv file.
        """
        documents = self.LPI_loader()
        

        logger.info(f"Connected to the weaviate embedded instance: {self.client.is_ready()}")

        # Create the vector database
        vector_store = WeaviateVectorStore(
            weaviate_client = self.client, 
            index_name = self.index_name
        )

        # Set up the storage for the embeddings
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # Setup the index
        # build VectorStoreIndex that takes care of chunking documents
        # and   encoding chunks to embeddings for future retrieval

        logger.info(f"Creating the {self.index_name} index")
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
        logger.info(f"The {self.index_name} index has been created")
        return index
