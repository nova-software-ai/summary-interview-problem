from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
import sys
import csv
import asyncio
sys.setrecursionlimit(3000)

# assume no cycles in the graph

class AbapProgram(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    uri: str = Field(description="The URI of the ABAP object.")
    display_name: str = Field(description="The display name of the ABAP object.")
    type: str = Field(description="The type of the ABAP object.")
    package_name: str = Field(description="The package name of the ABAP object.")
    source_code: str = Field(description="The source code of the ABAP object.")
    summary: Optional[str] = Field(description="A LLM-created summary of the ABAP object.")

class AbapProgramRelation(BaseModel):
    abap_program_id: str = Field(description="The ID of the ABAP program.")
    relation_type: str = Field(description="The type of the relation.")
    related_abap_program_id: str = Field(description="The ID of the related ABAP program.")

async def get_single_summary_for_program_with_no_relations(program: AbapProgram) -> str:    
    # Add fake delay to simulate LLM API call
    await asyncio.sleep(0.5)

    # mocked summary
    return f"""
This program ({program.display_name}) is a {program.type} in the {program.package_name} package.
    """

async def get_single_summary_for_program_with_relations(program: AbapProgram, related_programs: List[AbapProgram]) -> str:
    for related_program in related_programs:
        if not related_program.summary:
            raise Exception(f"Summary for {related_program.display_name} is not set")
    
    # mocked summary
    relations = ""
    for related_program in related_programs:
        relations += f" - {related_program.display_name} ({related_program.type})"
        
    # Add fake delay to simulate LLM API call
    await asyncio.sleep(0.5)
        
    return f"""
This program ({program.display_name}) is a {program.type} in the {program.package_name} package.

It has the following relations:
{relations}
    """


def load_data():
    # First load all programs
    programs = []
    with open('abap_programs.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            programs.append(AbapProgram(
                id=row['\ufeff"id"'],
                display_name=row['display_name'],
                package_name=row['package_name'],
                type=row['type'],
                uri='',
                summary='',
                source_code=''
            ))
    
    # Create a set of valid program IDs for quick lookup
    valid_program_ids = {program.id for program in programs}
    
    # Now load relations, checking if both IDs exist in the programs
    relations = []
    with open('abap_program_relations.csv') as f:
        reader = csv.DictReader(f)
        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue
                
            abap_program_id = row['\ufeffabap_program_id']
            related_abap_program_id = row['related_abap_program_id']
            
            # Only add the relation if both IDs exist in the programs list
            if abap_program_id in valid_program_ids and related_abap_program_id in valid_program_ids:
                relations.append(AbapProgramRelation(
                    abap_program_id=abap_program_id,
                    relation_type=row['relation_type'], 
                    related_abap_program_id=related_abap_program_id
                ))

    return relations, programs



# TO-DO:
# implement this method
async def get_summaries_for_all_programs():
    # Load relations from CSV
    relations, programs = load_data()

    pass


# PART2:
# system design for dealing with very long FORMs

if __name__ == "__main__":
    asyncio.run(get_summaries_for_all_programs())