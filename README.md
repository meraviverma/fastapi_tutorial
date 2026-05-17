# fastapi_tutorial

Below is a polished, well-structured Markdown version of your Pydantic guide. It’s formatted for readability, with headings, code-style inline notes, callouts, and concise sections suitable for README files, documentation pages, or a blog post.

***

# Pydantic: A Comprehensive Guide to Data Validation in Python

## Executive Summary
Pydantic is a powerful Python library for data validation and settings management using Python type annotations. While Python is dynamically typed, which increases flexibility, that same flexibility can cause runtime errors in production systems. Pydantic enforces type hints at runtime and provides a robust framework for complex validation, reducing repetitive manual checks and boilerplate code.

Pydantic follows a three-step workflow: define a model (schema), instantiate the model with raw data (triggering validation and optional type coercion), and use the validated object. Key features include custom data types (e.g., emails, URLs), field-level and model-level validators, computed fields, nested models, and high performance in Pydantic V2 thanks to a Rust core.

***

## 1. The Core Problem: Dynamic Typing and Validation Scaling

In standard Python, variables can change type at runtime (e.g., an integer becomes a string), which is convenient but risky in production. Incorrectly formatted data can propagate into databases or APIs and cause subtle bugs.

### 1.1 Type Hinting vs. Type Enforcement
- Type hints (e.g., `age: int`) are informative only; Python won’t prevent passing a string where an integer is expected.
- Without Pydantic, developers rely on manual checks:
  - Example: `if type(age) != int: raise TypeError`
- Manual checks are error-prone and verbose.

### 1.2 The Scalability Issue
Manual validation becomes unmanageable because:
- Redundancy: validation code repeats across functions (e.g., `insert_data`, `update_data`).
- Maintenance: adding a new field forces updates in multiple places.
- Complexity: format checks (emails, ranges) require complex regex and boilerplate.

***

## 2. The Pydantic Workflow

Pydantic streamlines validation with a clear three-step process based around `BaseModel`.

1. Build a Model  
   Define a class inheriting from `BaseModel` and declare fields with type hints and constraints.

2. Instantiate  
   Create an object by passing raw data (e.g., a `dict`). Pydantic validates types and values automatically.

3. Utilize  
   Use the validated object in your code. If data is invalid, Pydantic raises `ValidationError` before object creation.

***

## 3. Data Schema Definition

Pydantic models let you precisely control structure, from simple primitives to nested complex containers.

### 3.1 Field Requirements and Defaults
- Required fields: fields declared without a default are mandatory.
- Optional fields: use `Optional[...]` and provide a default (commonly `None`).
- Default values: e.g., `married: bool = False`. If absent in input, defaults are used.

### 3.2 Type Coercion
- Pydantic performs smart coercion. Example: `age: int` with input `"30"` becomes integer `30` automatically.

### 3.3 Complex and Custom Types
- Containers: `List[str]`, `Dict[str, str]` enforce types for elements.
- Specialized types: `EmailStr`, `AnyUrl` validate common formats.

***

## 4. Advanced Validation Techniques

Pydantic supports richer validation and metadata attachment for business logic and documentation.

### 4.1 The `Field` Function and `Annotated`
Use `Field` (often with `Annotated`) to add constraints and metadata:
- Numeric constraints: `gt`, `lt`, `ge`, `le`.
- String constraints: `max_length`, `min_length`.
- Metadata: `title`, `description`, `examples` (useful for auto API docs like FastAPI).
- Strict mode: `Field(..., strict=True)` disables coercion and enforces exact types.

### 4.2 Field Validators
- Use `@field_validator` to apply custom logic to single fields.
- Use cases:
  - Domain checks (e.g., ensure email domain is `hdfc.com`).
  - Transformations (e.g., uppercase a string).
- Modes:
  - `before`: validate raw input prior to built-in coercion.
  - `after` (default): validate after coercion into the target type.

### 4.3 Model Validators
- Use `@model_validator` when validation relies on multiple fields.
- Example: “If `age > 60`, `emergency_contact` must be provided.” This requires model-wide access.

***

## 5. Architectural Features

### 5.1 Computed Fields
- Computed fields are derived at runtime from other fields.
- Example: calculate `bmi` from `height` and `weight` using `@computed_field` and `@property`.

### 5.2 Nested Models
- Models can embed other models for hierarchical structures (e.g., an `Address` model inside a `Patient` model).
- Benefits:
  - Reusability
  - Readability
  - Automatic validation of nested data

***

## 6. Data Exportation

Pydantic models can be converted back to common formats:
- `model_dump()` — returns a Python `dict`.
- `model_dump_json()` — returns a JSON string.

### 6.1 Export Controls
- `include`: export only specified fields.
- `exclude`: omit listed fields.
- `exclude_unset`: export only fields explicitly provided during creation (omitting defaults).

***

## 7. Performance and Compatibility

- Pydantic V2 uses a Rust core for its validation engine, yielding significant speed improvements.
- It’s a common foundation for modern Python libraries (e.g., FastAPI) and is widely used in data science for ML pipelines and configuration management (including YAML).

***

## 8. Conclusion

Pydantic converts Python’s flexible typing into a structured, production-ready environment. Centralizing validation in models removes boilerplate, ensures data integrity, and creates self-documenting schemas. Whether validating API inputs or cleaning ML pipeline data, Pydantic is an essential tool for robust, maintainable codebases.

***