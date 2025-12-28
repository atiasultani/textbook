# Data Model: Physical AI Chapters

## Overview
Data model for the Physical AI textbook chapters, defining the structure and components of educational content.

## Content Entities

### Chapter
- **name**: String (e.g., "Foundations of Physical AI")
- **number**: Integer (1-3)
- **learning_objectives**: Array of String
- **sections**: Array of Section
- **examples**: Array of Example
- **questions_answers**: Array of QA_Pair
- **exercises**: Array of Exercise
- **activities**: Array of Activity
- **summary**: String
- **visual_aids**: Array of Asset_Reference

### Section
- **title**: String
- **content**: String (Markdown format)
- **learning_outcomes**: Array of String
- **duration_estimate**: Integer (minutes)

### Example
- **title**: String
- **scenario**: String (real-world context)
- **problem**: String
- **solution**: String
- **code_implementation**: Optional String (if applicable)
- **visual_representation**: Optional Asset_Reference

### QA_Pair
- **question**: String
- **answer**: String
- **difficulty_level**: Enum (Basic, Intermediate, Advanced)
- **tags**: Array of String (concept tags)

### Exercise
- **title**: String
- **description**: String
- **instructions**: String
- **expected_outcome**: String
- **difficulty_level**: Enum (Basic, Intermediate, Advanced)
- **estimated_time**: Integer (minutes)
- **solution**: String

### Activity
- **title**: String
- **description**: String
- **materials_needed**: Array of String
- **instructions**: String (step-by-step)
- **expected_outcome**: String
- **duration**: Integer (minutes)
- **prerequisites**: Array of String
- **assessment_criteria**: Array of String

### Asset_Reference
- **filename**: String
- **alt_text**: String
- **type**: Enum (image, diagram, video, animation)
- **caption**: String

## Relationships
- Chapter contains multiple Sections
- Chapter contains multiple Examples
- Chapter contains multiple QA_Pairs
- Chapter contains multiple Exercises
- Chapter contains multiple Activities
- Section may reference multiple Asset_References

## Validation Rules
- Each Chapter must have 1-3 learning objectives
- Each Chapter must contain 3-7 Sections
- Each Chapter must include 5+ Examples
- Each Chapter must include 10+ QA_Pairs
- Each Chapter must include 3+ Exercises
- Each Chapter must include 2+ Activities
- All content must align with Physical AI concepts
- All examples must be technically accurate
- All exercises must have verifiable solutions