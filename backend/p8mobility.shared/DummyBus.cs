using System;
using System.Security.Cryptography.X509Certificates;

namespace p8_shared;

public class DummyBus
{
    public Guid Id { get; set; }
    public double Position { get; set; }
    public double Speed { get; set; }

    public DummyBus(double position, double speed)
    {
        Position = position;
        Speed = speed;
    }
    public DummyBus(Guid id, double position, double speed)
    {
        Id = id;
        Position = position;
        Speed = speed;
    }
}