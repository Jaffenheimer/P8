using Moq;
using MySql.Data.MySqlClient;
using NUnit.Framework;
using p8_restapi.StateController;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace p8mobility.test
{
    [TestFixture]
    public class Tests
    {
        Mock<IBusStopRepository> busStopRepositoryMock = new();
        Mock<IRouteRelationsRepository> routeRelationsRepositoryMock = new();
        StateController sc = new StateController();

        [SetUp] 
        public void SetUp() {
            routeRelationsRepositoryMock.Setup(x => x.GetRouteIds()).Returns(Task.FromResult(new System.Collections.Generic.List<Guid>()));
            sc.Init(busStopRepositoryMock.Object, routeRelationsRepositoryMock.Object);
        }
        [Test]
        public void AddBusToStateSuccess()
        {
            //Arrange
            Bus bus = new Bus(0, 0, Guid.NewGuid(), Guid.NewGuid());

            //Act
            sc.AddBus(bus);

            //Assert
            Assert.True(sc.GetBus(bus.Id).Equals(bus));
        }

        [Test]
        public void DeleteBusFromStateSuccess()
        {
            //Arrange
            Bus bus = new Bus(0, 0, Guid.NewGuid(), Guid.NewGuid());
            Bus bus2 = new Bus(0, 0, Guid.NewGuid(), Guid.NewGuid());
            sc.AddBus(bus);

            //Act
            sc.DeleteBus(bus.Id);

            //Assert
            Assert.AreEqual(sc.GetState().Buses.Count(), 1);
        }

        [TearDown] 
        public void TearDown() {
            sc.Stop();
        }
    }
}