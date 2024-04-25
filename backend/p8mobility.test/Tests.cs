using Microsoft.VisualStudio.TestPlatform.ObjectModel;
using Moq;
using MySql.Data.MySqlClient;
using NUnit.Framework;
using p8_restapi.PusherService;
using p8_restapi.StateController;
using p8_shared;
using p8mobility.persistence.BusRepository;
using p8mobility.persistence.BusStopRepository;
using p8mobility.persistence.RouteRelationsRepository;
using PusherServer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace p8mobility.test
{
    [TestFixture]
    public class Tests
    {
        Mock<IBusStopRepository> busStopRepositoryMock = new();
        Mock<IRouteRelationsRepository> routeRelationsRepositoryMock = new();
        StateController sc = new StateController();
        Mock<IPusherService> pusherMock = new();

        [SetUp] 
        public void SetUp() {
            routeRelationsRepositoryMock.Setup(x => x.GetRouteIds()).Returns(Task.FromResult(new System.Collections.Generic.List<Guid>()));
            busStopRepositoryMock.Setup(x => x.GetAllBusStops()).Returns(Task.FromResult(new List<BusStop>() { new BusStop(Guid.Parse("d1eb0f95-2f04-4bdd-82d0-5a94dd402eea"), 59, 7, 25), new BusStop(Guid.Parse("efe4f617-45bb-46e1-8b8a-bd7cd10250de"), 11, 22, 42) }));
            sc.Init(busStopRepositoryMock.Object, routeRelationsRepositoryMock.Object);
        }
        [Test]
        public void RunStopStateSuccess()
        {
            StateController sc = new StateController();
            Mock<IPusherService> pusherMock = new();
            ////Arrange/Act/Assert
            new Thread (() => sc.Run(pusherMock.Object));
            var isRunning = sc.IsRunning; //Sets running to true
            var running = sc.Running;

            sc.Stop(); //Sets running to false
            var afterStop = sc.Running;
            Assert.AreNotEqual(running, afterStop);
            Assert.IsFalse(isRunning);
            Assert.IsTrue(running);
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
        [Test]
        public void GetStateSuccess()
        {
            //AAA
            var state = sc.GetState();
            Assert.NotNull(state);
        }
        

        [TestCase("d1eb0f95-2f04-4bdd-82d0-5a94dd402eea", 0)]
        [TestCase("efe4f617-45bb-46e1-8b8a-bd7cd10250de", 42)]
        [Test]
        public void UpdatePeopleCountSucces(Guid busStopId, int peopleCount)
        {
            //AAA
            var updatedBusStop = sc.UpdatePeopleCount(busStopId, peopleCount);
            Assert.That(updatedBusStop.PeopleCount == peopleCount);
        }

        [TearDown] 
        public void TearDown() {
            sc.Stop();
        }
    }
}