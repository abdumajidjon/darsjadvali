"""Database setup script - PostgreSQL connection test and database creation"""

import asyncio
import asyncpg
from app.config import settings
import sys


async def test_connection():
    """Test PostgreSQL connection"""
    print("Testing PostgreSQL connection...")
    
    # Parse DATABASE_URL
    db_url = settings.database_url
    if not db_url.startswith("postgresql+asyncpg://"):
        print("❌ Invalid DATABASE_URL format")
        return False
    
    # Remove asyncpg prefix
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    try:
        # Try to connect
        conn = await asyncpg.connect(db_url)
        print("[OK] Connection successful!")
        
        # Get database name
        db_name = await conn.fetchval("SELECT current_database()")
        print(f"Connected to database: {db_name}")
        
        # Check if tables exist
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        if tables:
            print(f"Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table['table_name']}")
        else:
            print("No tables found. Run migrations: alembic upgrade head")
        
        await conn.close()
        return True
        
    except asyncpg.exceptions.InvalidPasswordError:
        print("[ERROR] Invalid password. Please check your .env file")
        print(f"   DATABASE_URL: {settings.database_url.split('@')[0]}@...")
        return False
    except asyncpg.exceptions.InvalidCatalogNameError as e:
        print(f"[ERROR] Database does not exist: {e}")
        print("Creating database...")
        return await create_database()
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        print("\nPossible solutions:")
        print("   1. Check PostgreSQL is running")
        print("   2. Verify DATABASE_URL in .env file")
        print("   3. Check username and password")
        print("   4. Verify port (5432 for PostgreSQL 15, 5433 for PostgreSQL 18)")
        return False


async def create_database():
    """Create database if it doesn't exist"""
    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    # Extract database name
    try:
        # Parse URL: postgresql://user:pass@host:port/dbname
        parts = db_url.split("@")
        if len(parts) != 2:
            print("[ERROR] Invalid DATABASE_URL format")
            return False
        
        auth_part = parts[0].replace("postgresql://", "")
        host_part = parts[1]
        
        username = auth_part.split(":")[0]
        password = ":".join(auth_part.split(":")[1:]) if ":" in auth_part else ""
        
        host_port = host_part.split("/")
        host_port_part = host_port[0]
        db_name = host_port[1] if len(host_port) > 1 else "schedule_bot"
        
        host = host_port_part.split(":")[0]
        port = int(host_port_part.split(":")[1]) if ":" in host_port_part else 5432
        
        # Connect to postgres database to create new database
        postgres_url = f"postgresql://{username}:{password}@{host}:{port}/postgres"
        
        try:
            conn = await asyncpg.connect(postgres_url)
            print(f"✅ Connected to PostgreSQL server")
            
            # Check if database exists
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", db_name
            )
            
            if exists:
                print(f"ℹ️  Database '{db_name}' already exists")
                await conn.close()
                return True
            
            # Create database
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Database '{db_name}' created successfully!")
            await conn.close()
            return True
            
        except asyncpg.exceptions.InvalidPasswordError:
            print("[ERROR] Invalid password. Cannot create database.")
            print("   Please check your .env file and update DATABASE_URL")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to create database: {e}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error parsing DATABASE_URL: {e}")
        return False


async def main():
    """Main function"""
    print("=" * 50)
    print("PostgreSQL Database Setup")
    print("=" * 50)
    print()
    
    success = await test_connection()
    
    print()
    if success:
        print("[OK] Database setup complete!")
        print("Next steps:")
        print("   1. Run migrations: alembic upgrade head")
        print("   2. Start application: py -3.11 main.py")
    else:
        print("[ERROR] Database setup failed!")
        print("Please fix the issues above and try again")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
