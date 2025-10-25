namespace PersonaConfig.Infraestructure.Exceptions
{
    public class PersonaServiceException(string message) : Exception(message)
    {
        public static void ThrowUnauthorized(string message)
            => throw new PersonaServiceUnauthorizedException(message);

        public static void ThrowNotFound(string message)
            => throw new PersonaServiceNotFoundException(message);

        public static void ThrowConflict(string message)
            => throw new PersonaServiceConflictException(message);
    }

    public class PersonaServiceUnauthorizedException(string message) : PersonaServiceException(message) { }

    public class PersonaServiceNotFoundException(string message) : PersonaServiceException(message) { }

    public class PersonaServiceConflictException(string message) : PersonaServiceException(message) { }
}