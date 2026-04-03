# Marina's Garden: API Service 🤖

**Live API Endpoint:** [Play Marina's Garden](https://garden.thomaspercival.dev/)  
**Frontend Client Repository:** [Link to frontend](https://github.com/tpercival01/Marinas-Garden-Frontend)

This is the API service for Marina's Digital Garden. It is a Python-based microservice built with FastAPI. It handles all database CRUD operations, secure authentication routing, and integrates directly with the Groq API to provide generative AI botany data.

## 🌟 API Features

- **The AI Botanist**: Integrates with Groq (`llama-3.3-70b-versatile`). When a seed is planted, the AI dynamically generates precise watering frequencies, sunlight requirements, and highly specific, whimsical facts based on the plant's species and custom name.
- **PostgreSQL Database Management**: Connects directly to Supabase to handle the insertion, deletion, and updating of plant states (like the `last_watered` timestamp).
- **Automated User Profiling**: Utilizes PostgreSQL Database Triggers to automatically generate linked user profiles whenever a new authentication record is created in Supabase.
- **Secure RESTful Endpoints**: Built with FastAPI and Pydantic for strict data validation and schema definitions.

## 🛠️ Tech Stack

- **Framework**: FastAPI, Python, Uvicorn
- **Data Validation**: Pydantic models
- **AI Integration**: Groq API
- **Database**: Supabase (PostgreSQL)
- **Hosting**: Render

## 🚀 Local Development Setup

To run the backend server locally to support the Next.js client:

### 1. Install Dependencies
Navigate to the backend directory and install the Python packages:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```text
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Start the Server
Run the Uvicorn server with hot-reloading enabled:
```bash
uvicorn main:app --reload
```
The API will be running on `http://127.0.0.1:8000`. You can view the automatically generated Swagger documentation at `http://127.0.0.1:8000/docs`.

## 🗄️ Database Schema & Triggers
To properly handle authentication without email verification, this backend requires a PostgreSQL trigger on the Supabase database:
```sql
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, display_name)
  values (new.id, split_part(new.email, '@', 1));
  return new;
end;
$$ language plpgsql security definer;

create or replace trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
```

## 🗺️ V2.0 Roadmap (Backend Focus)
- **The Compost Graveyard**: Transition the HTTP `DELETE` route to a soft-delete (status patch) so users can retain the history of dead/uprooted plants.
- **Weather API Integration**: Connect a Python weather API to dynamically adjust the Groq AI's `water_frequency_days` output based on the user's local humidity and rainfall.
- **Endpoint Security**: Add FastAPI dependency injection to verify the Supabase JWT tokens in the request headers rather than relying purely on client-provided User IDs.
