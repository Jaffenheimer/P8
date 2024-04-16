using NUnit.Framework;
using p8_shared;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;

namespace p8mobility.test
{
    [TestFixture]
    class HelperTests
    {
        HelperFunctions h = new HelperFunctions();
        SHA256 sha256 = SHA256.Create();

        [Test]
        public void GenerateHashSuccess()
        {
            //Arrange
            var testPass = "MegetHemmeligtPassword";

            //Act
            var hash = h.GenerateHash(testPass);
            var decodedHash = sha256.ComputeHash(Encoding.UTF8.GetBytes(testPass));
            StringBuilder sb = new StringBuilder();
            foreach (byte b in decodedHash)
                sb.Append(b.ToString("X2"));

            //Assert
            Assert.AreEqual(hash, sb.ToString());
        }
    }
}
