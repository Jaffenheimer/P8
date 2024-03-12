using System.Reflection;
using DbUp;

namespace p8_dbup
{
    class Program
    {
        static int Main(string[] args)
        {
            var connectionString = "";

            var sqlUpgrader =
                DeployChanges.To
                    .MySqlDatabase(connectionString)
                    .WithScriptsEmbeddedInAssembly(Assembly.GetExecutingAssembly())
                    .LogToConsole()
                    .Build();

            sqlUpgrader.PerformUpgrade();

            return 0;
        }
    }
}