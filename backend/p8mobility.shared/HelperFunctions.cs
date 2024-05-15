using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;
using Microsoft.VisualBasic.FileIO;

namespace p8_shared;

public class HelperFunctions
{
    /// <summary>
    /// Generates a hash from a string
    /// </summary>
    /// <param name="source"></param>
    /// <returns>Returns the hashed value as a string</returns>
    public virtual string GenerateHash(string source)
    {
        //Generates hash from string
        SHA256 sha256 = SHA256.Create();
        byte[] tmpSource = Encoding.UTF8.GetBytes(source);
        var tmpHash = sha256.ComputeHash(tmpSource);

        //Assembles the hash as a string from the byte[]
        StringBuilder sb = new StringBuilder();
        foreach (byte b in tmpHash)
            sb.Append(b.ToString("X2"));

        return sb.ToString();
    }

    /// <summary>
    /// Generates a salt
    /// </summary>
    /// <returns>Returns a salt as a string</returns>
    public virtual string GenerateSalt()
    {
        var random = RandomNumberGenerator.Create();
        byte[] buffer = new byte[32];
        random.GetBytes(buffer);
        string salt = BitConverter.ToString(buffer);
        return salt;
    }
    
    // Read a csv file and return the content as an object
    public static SUMOStateSpaceObject ReadCsv()
    {
        var simulation = new SUMOStateSpaceObject(new List<double>(), new List<double>());
        int counter = 0;
        using (TextFieldParser parser = new TextFieldParser("../run.csv"))
            
            while (!parser.EndOfData)
            {
                //Processing row
                string[]? fields = parser.ReadFields();

                if (fields != null)
                {
                    simulation.AverageWaitTime.Add(double.Parse(fields[0]));
                    simulation.AveragePeopleAtBusStops.Add(double.Parse(fields[1]));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[3]), double.Parse(fields[2])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[5]), double.Parse(fields[4])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[7]), double.Parse(fields[6])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[9]), double.Parse(fields[8])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[9]), double.Parse(fields[10])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[11]), double.Parse(fields[12])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[13]), double.Parse(fields[14])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[15]), double.Parse(fields[16])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[17]), double.Parse(fields[18])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[19]), double.Parse(fields[20])));
                    simulation.Buses[counter].Add(new DummyBus(double.Parse(fields[21]), double.Parse(fields[22])));
                    counter++;
                }
            }

        return simulation;
    }
    
    public double CalcAvaragePeopleAtBusStops(List<BusStop> busStops)
    {
        var sum = 0.0;
        foreach (var busStop in busStops)
        {
            sum += busStop.PeopleCount;
        }
        
        return sum / busStops.Count;
    }
}