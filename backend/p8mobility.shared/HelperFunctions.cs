using System;
using System.Collections.Generic;
using System.Globalization;
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
        var simulation = new SUMOStateSpaceObject(new List<double>(), new List<double>(), new List<List<DummyBus>>());
        var firstLine = true;
        using (TextFieldParser parser = new TextFieldParser("../run.csv"))
            while (!parser.EndOfData)
            {
                //Processing row
                parser.Delimiters = new[] { "," };
                simulation.StateCount++;
                if (firstLine) { parser.ReadLine(); firstLine = false; }
                string[]? fields = parser.ReadFields();
                var busList = new List<DummyBus>();
                if (fields != null && fields.Length != 0)
                {
                    simulation.AverageWaitTime.Add(ParseDouble(fields[0]));
                    simulation.AveragePeopleAtBusStops.Add(ParseDouble(fields[1]));
                    busList.Add(new(ParseDouble(fields[3]), ParseDouble(fields[2])));
                    busList.Add(new DummyBus(ParseDouble(fields[5]), ParseDouble(fields[4])));
                    busList.Add(new DummyBus(ParseDouble(fields[7]), ParseDouble(fields[6])));
                    busList.Add(new DummyBus(ParseDouble(fields[9]), ParseDouble(fields[8])));
                    busList.Add(new DummyBus(ParseDouble(fields[11]), ParseDouble(fields[10])));
                    busList.Add(new DummyBus(ParseDouble(fields[13]), ParseDouble(fields[12])));
                    busList.Add(new DummyBus(ParseDouble(fields[15]), ParseDouble(fields[14])));
                    busList.Add(new DummyBus(ParseDouble(fields[17]), ParseDouble(fields[16])));
                    busList.Add(new DummyBus(ParseDouble(fields[19]), ParseDouble(fields[18])));
                    busList.Add(new DummyBus(ParseDouble(fields[21]), ParseDouble(fields[20])));
                    simulation.Buses.Add(busList);

                }
            }

        return simulation;
    }
    
    
    private static double ParseDouble(string value)
    {
        return double.Parse(value, CultureInfo.InvariantCulture);
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