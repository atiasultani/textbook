# Data Model: ROS 2 Fundamentals Educational Content

## Entity: ROS 2 Chapter
- **name**: string (e.g., "Core ROS 2 Concepts", "Advanced ROS 2 Development", "ROS 2 Ecosystem and Integration")
- **slug**: string (URL-friendly identifier)
- **content**: markdown string (main chapter content)
- **learning_objectives**: array of strings (what students should learn)
- **examples**: array of code examples with descriptions
- **exercises**: array of hands-on exercises
- **questions**: array of assessment questions with answers
- **physical_activities**: array of practical activities
- **images**: array of image references with alt text
- **length_pages**: integer (target 10-15)
- **difficulty_level**: enum (beginner, intermediate, advanced)

## Entity: Learning Objective
- **id**: string (unique identifier)
- **description**: string (what student should be able to do)
- **chapter_id**: string (reference to parent chapter)
- **assessment_method**: string (how this will be tested)

## Entity: Practical Exercise
- **id**: string (unique identifier)
- **title**: string (exercise name)
- **description**: string (what to do)
- **requirements**: array of strings (what is needed)
- **steps**: array of strings (step-by-step instructions)
- **expected_outcome**: string (what should happen)
- **difficulty**: enum (easy, medium, hard)
- **chapter_id**: string (reference to parent chapter)

## Entity: Assessment Question
- **id**: string (unique identifier)
- **question_text**: string (the question)
- **answer_text**: string (the answer)
- **question_type**: enum (multiple_choice, short_answer, practical)
- **difficulty**: enum (easy, medium, hard)
- **chapter_id**: string (reference to parent chapter)

## Entity: Physical Activity
- **id**: string (unique identifier)
- **title**: string (activity name)
- **description**: string (what to do)
- **materials_needed**: array of strings (what is required)
- **steps**: array of strings (instructions)
- **learning_outcome**: string (what is learned)
- **chapter_id**: string (reference to parent chapter)

## Entity: Code Example
- **id**: string (unique identifier)
- **title**: string (example name)
- **code_snippet**: string (the actual code)
- **explanation**: string (what the code does)
- **chapter_id**: string (reference to parent chapter)
- **language**: string (e.g., "python", "c++")