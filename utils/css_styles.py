course_card = """
    <style>
        /* Estilos generales */
        .main {
            background-color: #f8f9fa;
            padding: 20px;
        }

        /* Estilos para tarjetas de cursos */
        .course-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }

        .course-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }

        .course-title {
            color: #2c3e50;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .course-description {
            color: #555;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }

        .course-id {
            background-color: #e9ecef;
            color: #495057;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            display: inline-block;
        }
        
        /* Estilos para botones */
        .custom-button {
            background-color: #1e88e5;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .custom-button:hover {
            background-color: #1565c0;
        }

        .return-button {
            background-color: #6c757d;
        }

        .return-button:hover {
            background-color: #495057;
        }
    </style>
    """