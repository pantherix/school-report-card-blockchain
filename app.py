import streamlit as st
import hashlib
import datetime
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   json.dumps(self.data, sort_keys=True).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(block_data):
        return Block(
            index=block_data['index'],
            timestamp=datetime.datetime.fromisoformat(block_data['timestamp']),
            data=block_data['data'],
            previous_hash=block_data['previous_hash']
        )

def create_genesis_block():
    return Block(0, datetime.datetime.now(), {"Genesis": "Block"}, "0")

def create_next_block(last_block, data):
    this_index = last_block.index + 1
    this_timestamp = datetime.datetime.now()
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, data, this_hash)

# Initialize the blockchain
try:
    with open('blockchain.json', 'r') as f:
        blockchain = [Block.from_dict(block_data) for block_data in json.load(f)]
        previous_block = blockchain[-1]
except (FileNotFoundError, json.JSONDecodeError):
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

# Streamlit interface
st.title("🏫 School Report Card Blockchain")

student_name = st.text_input("Student Name")
subject = st.text_input("Subject")
grade = st.text_input("Grade")

if st.button("Add Report Card Entry"):
    if student_name and subject and grade:
        new_data = {
            "student": student_name,
            "subject": subject,
            "grade": grade,
            "timestamp": datetime.datetime.now().isoformat()
        }
        new_block = create_next_block(previous_block, new_data)
        blockchain.append(new_block)
        previous_block = new_block
        st.success("✅ Report card entry added successfully!")

        # Save blockchain to file
        with open('blockchain.json', 'w') as f:
            json.dump([block.to_dict() for block in blockchain], f, indent=4)
    else:
        st.error("⚠️ Please fill all fields before submitting.")

st.subheader("📦 Blockchain")
for block in blockchain:
    st.write(f"### Block #{block.index}")
    st.write(f"**Timestamp:** {block.timestamp}")
    st.json(block.data)
    st.write(f"**Previous Hash:**")
    st.code(block.previous_hash)
    st.write(f"**Hash:**")
    st.code(block.hash)
    st.markdown("---")
